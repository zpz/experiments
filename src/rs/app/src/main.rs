use datex::datex::weekday;


fn main() {
    println!("Hello, world!");
    let z = weekday(12345);
    println!("weekday {}", z);
    let z = weekday(123456);
    println!("weekday {}", z);
}
