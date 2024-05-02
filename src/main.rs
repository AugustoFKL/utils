#![warn(clippy::all, clippy::nursery, clippy::pedantic)]

use log::info;

use crate::utils::logging;

pub(crate) mod utils;

fn main() {
    logging::init().unwrap();

    info!("Hello, world!");
}
