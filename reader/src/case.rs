use serde::Deserialize;

#[derive(Deserialize)]
pub struct Case {
    pub data: String,
    pub lat: f64,
    pub long: f64,
    pub tipo: String
}