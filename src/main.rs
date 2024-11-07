use std::fmt::Display;
use std::process::exit;

use anyhow::{bail, Context, Result};
use reqwest::header::{HeaderMap, HeaderValue, ACCEPT, AUTHORIZATION};
use tracing::{error, instrument, warn};

use crate::default_labels::{EnvLabel, Label, TypeLabel, WorkflowLabel};

mod default_labels;
mod logging;

fn main() -> Result<()> {
    logging::setup();

    let owner = "AugustoFKL";
    let repo = "utils";
    let token = "";
    let labels = list_labels(owner, repo, token).context("Listing labels")?;

    for label in labels {
        delete_label(owner, repo, token, &label).context("Deleting label")?;
    }

    create_labels(owner, repo, token).context("Creating labels")?;

    Ok(())
}

#[instrument(skip_all)]
fn list_labels(owner: &str, repo: &str, token: &str) -> Result<Vec<String>> {
    let url = format!("https://api.github.com/repos/{owner}/{repo}/labels");

    let request = reqwest::blocking::Client::new()
        .get(url)
        .headers(default_headers(token));

    let response = request
        .send()
        .context("Sending request")?
        .json::<serde_json::Value>()
        .context("Parsing response as json")?;

    let response = response.as_array().context("Parsing response as array")?;

    let mut labels = Vec::with_capacity(response.len());
    for label in response {
        let name = label.get("name").and_then(|name| name.as_str());
        let Some(name) = name else {
            warn!("Name field missing, skipping");
            continue;
        };
        labels.push(name.to_owned());
    }

    Ok(labels)
}

#[instrument(skip_all, fields(label = label))]
fn delete_label(owner: &str, repo: &str, token: &str, label: &str) -> Result<()> {
    let url = format!("https://api.github.com/repos/{owner}/{repo}/labels/{label}");

    let request = reqwest::blocking::Client::new()
        .delete(url)
        .headers(default_headers(token));

    let response = request.send().context("Sending request")?;

    let status = response.status();
    if !status.is_success() {
        let body = response.text().unwrap_or_default();
        bail!("Failed to delete the label {label}: {status} {body}");
    }
    Ok(())
}

fn create_labels(owner: &str, repo: &str, token: &str) -> Result<()> {
    create_label(owner, repo, token, EnvLabel::CrossPlatform)?;
    create_label(owner, repo, token, EnvLabel::Linux)?;
    create_label(owner, repo, token, EnvLabel::MacOS)?;
    create_label(owner, repo, token, EnvLabel::Windows)?;

    create_label(owner, repo, token, TypeLabel::Build)?;
    create_label(owner, repo, token, TypeLabel::Chore)?;
    create_label(owner, repo, token, TypeLabel::Ci)?;
    create_label(owner, repo, token, TypeLabel::Docs)?;
    create_label(owner, repo, token, TypeLabel::Feat)?;
    create_label(owner, repo, token, TypeLabel::Fix)?;
    create_label(owner, repo, token, TypeLabel::Perf)?;
    create_label(owner, repo, token, TypeLabel::Refactor)?;
    create_label(owner, repo, token, TypeLabel::Revert)?;
    create_label(owner, repo, token, TypeLabel::Style)?;
    create_label(owner, repo, token, TypeLabel::Test)?;

    create_label(owner, repo, token, WorkflowLabel::Critical)?;
    create_label(owner, repo, token, WorkflowLabel::DiscussionNeeded)?;
    create_label(owner, repo, token, WorkflowLabel::GoodFirstIssue)?;
    create_label(owner, repo, token, WorkflowLabel::HelpWanted)?;
    create_label(owner, repo, token, WorkflowLabel::NeedsTriage)?;
    create_label(owner, repo, token, WorkflowLabel::UpForGrabs)?;

    Ok(())
}

#[instrument(skip_all, fields(label = label.to_string()))]
fn create_label<T>(owner: &str, repo: &str, token: &str, label: T) -> Result<()>
where
    T: Into<Label> + Display,
{
    let label = label.into();

    let url = format!("https://api.github.com/repos/{owner}/{repo}/labels");

    let request = reqwest::blocking::Client::new()
        .post(url)
        .json(&label)
        .headers(default_headers(token));

    let response = request.send().context("Failed to send request")?;
    let status = response.status();
    if !status.is_success() {
        let body = response.text().unwrap_or_default();
        error!("Failed to create the label {label}: {status} {body}");
        exit(1);
    }

    Ok(())
}

fn default_headers(token: &str) -> HeaderMap {
    let accept = HeaderValue::from_static("application/vnd.github+json");
    let Ok(authorization) = HeaderValue::from_str(&format!("Bearer {token}")) else {
        error!("Failed to create authorization header, provided token is invalid");
        exit(1);
    };
    let user_agent = HeaderValue::from_static("utils-cli");
    let api_version = HeaderValue::from_static("2022-11-28");

    let mut headers = HeaderMap::new();
    headers.insert(ACCEPT, accept);
    headers.insert(AUTHORIZATION, authorization);
    headers.insert("User-Agent", user_agent);
    headers.insert("X-GitHub-Api-Version", api_version);
    headers
}
