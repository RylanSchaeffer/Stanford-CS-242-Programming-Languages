/***************
 * NOTE:
 *   You can use `Sig`, `Pkt`,
 *   and anything defined in `src/prob3/client.rs` as `pub`  (e.g., `Client`),
 *   simply by `Sig`, `Pkt`,  `Client`, and so on without any prefixes.
 *   You can use the below helper function `pkts_remove`.
 ***************/

#[allow(unused_imports)]
use crate::prob2::client::*;
#[allow(unused_imports)]
use crate::prob2::msg::Pkt;
#[allow(unused_imports)]
use crate::prob2::server::Server;

/* pkts_remove(pkts, ids):
 *   - return a new vector that consists of packets in `pkts`
 *     whose id is not in `ids`. */
pub fn pkts_remove(pkts: &Vec<Pkt>, ids: &Vec<u32>) -> Vec<Pkt> {
    let mut pkts_res: Vec<Pkt> = pkts.clone();
    for id in ids.iter() {
        pkts_res.retain(|k| (*k).id != *id);
    }
    pkts_res
}

// Reliably send all given `pkts` to `server` using the TCP client implemented in Problem 2.
// DO NOT MODIFY THIS FUNCTION.
pub fn send_all(server: &mut Server, pkts: &Vec<Pkt>) {
    let client = Client::new();
    let syned = try_syn(server, client);
    let synacked = syned.send_ack(server);
    let synacked = try_pkts(server, synacked, pkts);
    let closed = try_close(server, synacked);
    let _ = closed.send_ack(server);
}

// Connect the client to the server. This function should ensure that the server acknowledges the
// connection before returning a Syned client.
fn try_syn(server: &mut Server, client: Initial) -> Syned {
    //===== BEGIN_CODE =====//
    let mut result = client;
    loop {
        println!("try_syn");
        match result.send_syn(server) {
            Ok(val) => return val,
            Err(val) => result = val,
        }
    }
    //===== END_CODE =====//
}

// Use the client to reliably send the given packets to the server. This function should ensure that
// all packets have been delivered to the server.
fn try_pkts(server: &mut Server, client: SynAcked, pkts: &Vec<Pkt>) -> SynAcked {
    //===== BEGIN_CODE =====//
    let mut original_pkts = pkts.clone();
    let mut remaining = client;
    loop {
        println!("try_pkts");
        remaining = remaining.send_pkts(server, &original_pkts);
        original_pkts = pkts_remove(&original_pkts, &remaining.ids_sent());
        if original_pkts.is_empty() {
            return remaining;
        }
    }
    //===== END_CODE =====//
}

// Close the client connection to the server. The function should ensure that the server
// acknowledges the end of the connection before returning a Closed client.
fn try_close(server: &mut Server, client: SynAcked) -> Closed {
    //===== BEGIN_CODE =====//
    let mut result = client;
    loop {
        println!("try_close");
        match result.send_close(server) {
            Ok(val) => return val,
            Err(val) => result = val,
        }
    }
    //===== END_CODE =====//
}
