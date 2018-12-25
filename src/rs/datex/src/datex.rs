extern crate ndarray;
use self::ndarray::{Array1, ArrayView1};


pub fn weekday(ts: i64) -> i64 
{
    let ts0: i64 = 1489363200;   // 2017-03-13 0:0:0 UTC, Monday
    let weekday0 = 1;       // ISO weekday: Monday is 1, Sunday is 7

    const DAY_SECONDS: i64 = 86400;
    const WEEK_SECONDS: i64 = 604800;

    let mut ts_delta = ts - ts0;
    if ts_delta < 0 {
        ts_delta += ((-ts_delta) / WEEK_SECONDS + 1) * WEEK_SECONDS;
    }

    let td: i64 = ts_delta % WEEK_SECONDS;
    let nday = td / DAY_SECONDS;
    let weekday: i64 = weekday0 + nday;
    if weekday > 7 {
        weekday - 7
    } else {
        weekday
    }
}


pub fn weekdays(x: ArrayView1<i64>) -> Array1<i64> {
    let mut out = Array1::<i64>::zeros(x.len());
    for (i, xx) in x.iter().enumerate() {
        out[i] = weekday(*xx);
    }
    out
}
