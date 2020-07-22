use serde::Deserialize;

#[derive(Deserialize)]
pub struct Region {
    pub denominazione_regione: String,
    pub lat: f64,
    pub long: f64
}