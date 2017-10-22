'use strict';

const fs = require('fs');
const express = require('express');
const bodyParser = require('body-parser')
const child_process = require('child_process');

const PORT = 10000;
const HOST = '0.0.0.0';
const BASE_DIRECTORY = "data/";
const SCRIPT_FILE_NAME = "main.js";

if (!fs.existsSync(BASE_DIRECTORY)) {
	fs.mkdirSync(BASE_DIRECTORY);
}

// App
const app = express();
app.use(express.urlencoded({ extended: false }))
app.post('/', (req, res) => {
	console.log(req.body);
	var directory = BASE_DIRECTORY+req.body.id + "/";
	fs.mkdirSync(directory);
	var scriptFile = directory + SCRIPT_FILE_NAME;
	var script = req.body.script;
	fs.writeFile(scriptFile, script, function(err) {
		if(err) {
			res.json({
				code: -1,
				stdout: '',
				stderr: err
			});
			return console.log(err);
		}
		var result = child_process.spawnSync("node", [SCRIPT_FILE_NAME], {encoding: 'utf-8', cwd: directory});
		var images = {};
		fs.readdirSync(directory).forEach(file => {
			if (file.endsWith(".jpg") || file.endsWith(".png")) {
				images[file]=fs.readFileSync(directory+file, 'base64');
			}
		});
		child_process.exec("rm -fr " + directory, function(err, stdout, stderr) {
			console.log(directory + " is cleaned.");
		});
		return res.json({
			code: result.status,
			stdout: result.stdout,
			stderr: result.stderr,
			images: images
		});
	});
});

app.listen(PORT, HOST);
console.log("Running on http://"+HOST+":"+PORT);
