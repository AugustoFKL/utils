use tracing_subscriber::fmt::format::FmtSpan;
use tracing_subscriber::fmt::time::ChronoLocal;
use tracing_subscriber::FmtSubscriber;

pub fn setup() {
    let subscriber = FmtSubscriber::builder()
        .with_env_filter("augusto_utils=debug")
        .with_timer(ChronoLocal::new("%Y-%m-%d %H:%M:%S".to_owned()))
        .with_span_events(FmtSpan::ENTER)
        .with_target(false)
        .finish();

    tracing::subscriber::set_global_default(subscriber).expect("Setting default subscriber failed");
}
