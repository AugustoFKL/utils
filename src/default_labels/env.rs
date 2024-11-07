use std::fmt::{Display, Formatter, Result};

use crate::default_labels::LabelConvertible;

const BITTERSWEET: &str = "FE6F5E";
const GOLD: &str = "FFD700";
const MEDIUM_SPRING_GREEN: &str = "00FA9A";
const SLATE_BLUE: &str = "6A5ACD";

pub enum Label {
    CrossPlatform,
    Linux,
    MacOS,
    Windows,
}

impl LabelConvertible for Label {
    fn name(&self) -> &str {
        match self {
            Self::CrossPlatform => "env: cross-platform",
            Self::Linux => "env: linux",
            Self::MacOS => "env: macos",
            Self::Windows => "env: windows",
        }
    }

    fn description(&self) -> &str {
        match self {
            Self::CrossPlatform => "Affects multiple operating systems.",
            Self::Linux => "Pertaining to Linux-based systems.",
            Self::MacOS => "Exclusively for macOS-related topics.",
            Self::Windows => "Windows-specific issues or improvements.",
        }
    }

    fn color(&self) -> &str {
        match self {
            Self::CrossPlatform => BITTERSWEET,
            Self::Linux => MEDIUM_SPRING_GREEN,
            Self::MacOS => SLATE_BLUE,
            Self::Windows => GOLD,
        }
    }
}

impl Display for Label {
    fn fmt(&self, f: &mut Formatter<'_>) -> Result {
        write!(f, "{}", self.name())
    }
}
