#![feature(specialization)]

#[macro_use]
extern crate pyo3;

use pyo3::prelude::*;

mod datex;


#[pyfunction]
fn weekday(x: i64) -> i64 {
    datex::weekday(x)
}


#[pymodule]
fn datex(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_wrapped(wrap_function!(weekday))?;

    Ok(())
}

