const cron = require('node-cron');
const { exec } = require('child_process');

const dns = require('node:dns');
dns.setDefaultResultOrder('ipv4first');
// Function to fetch CPE list from the given URL
async function fetchCpeList() {
    try {
        const response = await fetch('https://dionaditya-monitoring-22.deno.dev/api/trpc/cpe.get', { method: 'GET' });
        const data = await response.json();
        return data; // Assuming the response is an array of objects with 'ip' properties
    } catch (error) {
        console.error('Error fetching CPE list:', error);
        return [];
    }
}


// Function to run the Python and Node.js scripts
function runScripts(item) {
    return new Promise((res) => {
        // Run the Python script
        exec(`python main2.py --ip=${item.ip} --username=${item.username} --password=${item.password} --cmd="${item.command}"`, (error, stdout, stderr) => {
            if (error) {
                console.error(`Error running Python script for IP ${item.ip}:`, error);
                return;
            }
            console.log(`scraping data for IP ${item.ip}:`, stdout);

            // Run the Node.js script
            exec(`node table-extract.js --ip=${item.ip}`, (error, stdout, stderr) => {
                if (error) {
                    console.error(`Error running Node.js script for IP ${item.ip}:`, error);
                    return;
                }
                console.log(`processing data for IP ${item.ip}:`, stdout);

                exec(`python post.py --ip=${item.ip}`, (error, stdout, stderr) => {
                    if (error) {
                        console.error(`Error running Node.js script for IP ${item.ip}:`, error);
                        return;
                    }
                    res(true)
                    console.log(`updating data for IP ${item.ip}:`, stdout);
                });
            });
        });
    })
}

let isRunning = false 

// Schedule a task to run every 3 minutes
cron.schedule('*/2 * * * *', async () => {
    if (isRunning) {
        console.log('Previous task is still running. Skipping this execution.');
        return;
    }

    try {
        console.log('Starting new task - Fetching CPE list...');
        const cpeList = await fetchCpeList();
        console.log('Fetched CPE list:', cpeList);
    
        isRunning = true
        // Run the scripts for each IP in series
        for (const item of cpeList.result.data) {
            if (item.ip) {
                console.log('Running script for IP ' + item.ip);
                try {
                    await runScripts(item);
                } catch (error) {
                    console.error(`Error processing IP ${item.ip}:`, error);
                }
            } else {
                console.warn('No IP found for item:', item);
            }
        }
    } finally {
        isRunning = false;
        console.log('Task completed.');
    }
   
});

console.log('Cron job scheduled to run every 3 minutes.');

// Keep the script running
process.stdin.resume();