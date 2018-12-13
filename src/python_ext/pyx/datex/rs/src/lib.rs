#![feature(specialization)]
#![feature(custom_attribute)]

#[macro_use]

extern crate pyo3;
extern crate datex;

use pyo3::prelude::*;

use datex::datex::weekday as weekday_;


#[pyfunction]
fn weekday(x: i64) -> i64 {
    weekday_(x)
}


#[pymodule]
fn version01(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_wrapped(wrap_function!(weekday))?;

    Ok(())
}

