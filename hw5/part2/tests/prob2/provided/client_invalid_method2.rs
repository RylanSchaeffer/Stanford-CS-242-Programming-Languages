extern crate part2;
#[allow(unused_imports)]
use part2::prob2::msg::Pkt;
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
            let synacked = syned.send_ack(&mut server);
            let synacked = synacked.send_pkts(&mut server, &vec![Pkt{buf:'a', id:1}]);
             // `send_ack` method should be inaccessible in synacked state.
            synacked.send_ack(&mut server);
        }
    }
}
