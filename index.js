const GitHubRepoParser = require("github-repo-parser");
const fs = require("fs");
const { spawnSync } = require("child_process");

require("dotenv").config({ path: "../.env" });

const parser = new GitHubRepoParser(process.env.GITHUB_TOKEN);

const run_read_urls = async (dir, repo) => {
  const pythonProcess = await spawnSync("python", ["read_urls.py", dir, repo]);
  pythonProcess.stdout.on("data", (data) => {
    console.log(data);
  });
};

console.log("Initializing GitHubRepoParser...");
const get_repo_raw_urls = async (repo_name) => {
  let repo = repo_name.split("/")[4];
  let dir = repo_name.split("/")[3];
  console.log("Starting data collection for repository:", repo);
  const urls = await parser.collectData(repo_name);
  const stringified_urls = JSON.stringify(urls);
  fs.mkdirSync(`githubSources/${dir}`);
  fs.mkdirSync(`githubSources/${dir}/documentation`);
  fs.writeFileSync(
    `githubSources/${dir}/${repo}.json`,
    stringified_urls,
    "utf-8"
  );
  fs.writeFileSync(
    `githubSources/${dir}/documentation/${repo}.json`,
    "",
    "utf-8"
  );
  console.log("Data collection complete! Initiating parser...");
  //run_read_urls(dir, repo);
};

let githubRepoURL = "https://github.com/saarthdeshpande/book-summarizer";

get_repo_raw_urls(githubRepoURL);
