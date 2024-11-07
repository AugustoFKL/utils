use std::fmt::{Display, Formatter, Result};

use crate::default_labels::LabelConvertible;

const CORNFLOWER_BLUE: &str = "6495ED";
const DARK_ORANGE: &str = "FF8C00";
const FIREBRICK: &str = "B22222";
const HOT_PINK: &str = "FF69B4";
const ORCHID: &str = "DA70D6";
const TURQUOISE: &str = "40E0D0";

pub enum Label {
    Critical,
    DiscussionNeeded,
    GoodFirstIssue,
    HelpWanted,
    NeedsTriage,
    UpForGrabs,
}

impl LabelConvertible for Label {
    fn name(&self) -> &str {
        match self {
            Self::Critical => "workflow: critical",
            Self::DiscussionNeeded => "workflow: discussion-needed",
            Self::GoodFirstIssue => "workflow: good-first-issue",
            Self::HelpWanted => "workflow: help-wanted",
            Self::NeedsTriage => "workflow: needs-triage",
            Self::UpForGrabs => "workflow: up-for-grabs",
        }
    }

    fn description(&self) -> &str {
        match self {
            Self::Critical => "High-priority, severe impact issues.",
            Self::DiscussionNeeded => "Requires collective decision-making.",
            Self::GoodFirstIssue => "Suitable for new contributors.",
            Self::HelpWanted => "Open call for community contributors.",
            Self::NeedsTriage => "New, unaddressed issues for review.",
            Self::UpForGrabs => "Ready for immediate work, not urgent.",
        }
    }

    fn color(&self) -> &str {
        match self {
            Self::Critical => FIREBRICK,
            Self::DiscussionNeeded => CORNFLOWER_BLUE,
            Self::GoodFirstIssue => HOT_PINK,
            Self::HelpWanted => ORCHID,
            Self::NeedsTriage => TURQUOISE,
            Self::UpForGrabs => DARK_ORANGE,
        }
    }
}

impl Display for Label {
    fn fmt(&self, f: &mut Formatter<'_>) -> Result {
        write!(f, "{}", self.name())
    }
}
