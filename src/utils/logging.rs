use anyhow::Result;
use log4rs::config::Deserializers;

pub fn init() -> Result<()> {
    log4rs::init_file("./src/utils/logging.yaml", Deserializers::default())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_init() {
        assert!(init().is_ok());
    }
}
