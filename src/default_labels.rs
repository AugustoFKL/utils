use std::fmt::{Display, Formatter};

use serde::{Deserialize, Serialize};

pub use env::Label as EnvLabel;
pub use r#type::Label as TypeLabel;
pub use workflow::Label as WorkflowLabel;

mod env;
mod r#type;
mod workflow;

pub trait LabelConvertible {
    fn name(&self) -> &str;
    fn description(&self) -> &str;
    fn color(&self) -> &str;
}

#[derive(Debug, Serialize, Deserialize)]
pub struct Label {
    name: String,
    description: String,
    color: String,
}

impl Display for Label {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.name)
    }
}

impl<T> From<T> for Label
where
    T: LabelConvertible,
{
    fn from(item: T) -> Self {
        Self {
            name: item.name().to_owned(),
            description: item.description().to_owned(),
            color: item.color().to_owned(),
        }
    }
}
