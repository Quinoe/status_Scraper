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

parsedData = parsedData.map((i) => {
    let updated = {}

    Object.keys(i).forEach((name) => {
        updated[name.toLowerCase()] = i[name].join(' ')
    })

    updated['ip'] = ip

    return updated
})

// Write parsed data to a JSON file
FS.writeFileSync(outputFile, JSON.stringify(parsedData, null, 2), 'utf8');

console.log('Parsed data has been written to', outputFile);