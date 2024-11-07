use std::fmt::{Display, Formatter, Result};

use crate::default_labels::LabelConvertible;

const BROWN: &str = "A52A2A";
const CHOCOLATE: &str = "D2691E";
const DARK_RED: &str = "8B0000";
const DARK_TURQUOISE: &str = "00CED1";
const DEEP_PINK: &str = "FF1493";
const FOREST_GREEN: &str = "228B22";
const MEDIUM_PURPLE: &str = "9370DB";
const ORANGE_RED: &str = "FF4500";
const SEA_GREEN: &str = "2E8B57";
const STEEL_BLUE: &str = "4682B4";
const TOMATO: &str = "FF6347";

pub enum Label {
    Build,
    Chore,
    Ci,
    Docs,
    Feat,
    Fix,
    Perf,
    Refactor,
    Revert,
    Style,
    Test,
}

impl LabelConvertible for Label {
    fn name(&self) -> &str {
        match self {
            Self::Build => "type: build",
            Self::Chore => "type: chore",
            Self::Ci => "type: ci",
            Self::Docs => "type: docs",
            Self::Feat => "type: feat",
            Self::Fix => "type: fix",
            Self::Perf => "type: perf",
            Self::Refactor => "type: refactor",
            Self::Revert => "type: revert",
            Self::Style => "type: style",
            Self::Test => "type: test",
        }
    }

    fn description(&self) -> &str {
        match self {
            Self::Build => "Changes to the code building process.",
            Self::Chore => "Routine tasks and project maintenance.",
            Self::Ci => "Adjustments in CI processes and tools.",
            Self::Docs => "Exclusively for documentation updates.",
            Self::Feat => "For new functionalities or significant enhancements.",
            Self::Fix => "Used to correct and address software defects.",
            Self::Perf => "Enhances efficiency and speed of existing features.",
            Self::Refactor => "Internal code improvements without behavior change.",
            Self::Revert => "Undoing previous code changes.",
            Self::Style => "For non-functional code style improvements.",
            Self::Test => "Related to adding or improving test cases.",
        }
    }

    fn color(&self) -> &str {
        match self {
            Self::Build => DARK_RED,
            Self::Chore => ORANGE_RED,
            Self::Ci => DARK_TURQUOISE,
            Self::Docs => MEDIUM_PURPLE,
            Self::Feat => FOREST_GREEN,
            Self::Fix => DEEP_PINK,
            Self::Perf => STEEL_BLUE,
            Self::Refactor => CHOCOLATE,
            Self::Revert => BROWN,
            Self::Style => TOMATO,
            Self::Test => SEA_GREEN,
        }
    }
}

impl Display for Label {
    fn fmt(&self, f: &mut Formatter<'_>) -> Result {
        write!(f, "{}", self.name())
    }
}
