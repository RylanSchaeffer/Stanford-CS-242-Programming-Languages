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
             // `send_close` method should be inaccessible in syned state.
            syned.send_close(&mut server);
        }
    }
}
