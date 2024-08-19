var FS = require('fs');
var Parser = require('table-parser');

const minimist = require('minimist');

// Parse the command line arguments
const args = minimist(process.argv.slice(2));

// Get the IP address
const ip = args.ip;

var linux_ps = `./status-${ip}.log`;
var outputFile = `./status-${ip}.json`; // File path for the output JSON file

// Read the file and convert it to a string
var data = FS.readFileSync(linux_ps).toString();

function extractContent(fileContent) {
    // Split the content into lines
    const lines = fileContent.split('\n');

    // Find the starting point where the header is located
    let startIndex = 0;
    for (let i = 0; i < lines.length; i++) {
        const line = lines[i]
        if (line.includes("Link Speed") || line.includes("Link shutdn") || line.includes("Status    Vlan")) {
            startIndex = i;
            break;
        }
    }

    // Extract content starting from the header line
    const extractedContent = lines.slice(startIndex).join('\n');

    return extractedContent;
}

if (data.includes('Link Speed') || data.includes("Status    Vlan")) {
    data = extractContent(data)
    data = data.replace(/---- More ----/g, '')
    data = "\n\n\n" + data
}

if (data.includes('Link shutdn')) {
    data = extractContent(data)
    data = data.replace(/---- More ----/g, '')
    data = "\n\n\n" + data.split('\n').filter((line) => {
        return !line.includes('press ENTER')
    }).join('\n')
}
// Split the data into lines
var lines = data.split('\n');

// Remove the first and last lines
if (lines.length > 1) {
    lines = lines.slice(3)
    lines.pop();    // Remove the last line
}

// Join the remaining lines back into a single string
var modifiedData = lines.join('\n');

// Parse the modified data
var parsedData = Parser.parse(modifiedData);

const tableData = parsedData.map((i) => {
    let updated = {}

    Object.keys(i).forEach((name) => {
        updated[name.toLowerCase()] = i[name].join(' ')
    })

    updated['ip'] = ip

    return updated
})

tableData.forEach((item, i) => {
    if (item.port !== undefined && !item.port) {
       if (item.desc) {
        const previousItems = tableData.slice(0,i).map((item, index) => ({ ...item, index})).filter((item) => item.port)
        const targetIndex = previousItems[previousItems.length-1].index
        tableData[targetIndex].desc = tableData[targetIndex].desc + item.desc
       } else {
        Object.keys(item)
        .filter((key) => !['port', 'description', 'ip'].includes(key))
        .forEach((key) => {
            tableData[i - 1][key] = item[key]
        })
       }

    }


})

parsedData = tableData.filter((item) => {
    if (item.port !== undefined && item.port.length === 0) {
        return false
    }

    return true
})

// Write parsed data to a JSON file
FS.writeFileSync(outputFile, JSON.stringify(parsedData, null, 2), 'utf8');

console.log('Parsed data has been written to', outputFile);