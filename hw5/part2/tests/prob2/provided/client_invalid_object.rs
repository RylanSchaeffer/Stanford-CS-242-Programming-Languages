extern crate part2;
#[allow(unused_imports)]
use part2::prob2::server::{Server, RecvType};
#[allow(unused_imports)]
use part2::prob2::client::Client;

fn main() {
    let mut server: Server = Server::new(RecvType::All);
    let initial = Client::new();
    match initial.send_syn(&mut server) {
        Err(_syn_failed) =>
            assert!(false),
        Ok (syned) => {
            let _synacked = syned.send_ack(&mut server);
            // `syned` object should not be used again.
            syned.send_ack(&mut server);
        }
    }
}
