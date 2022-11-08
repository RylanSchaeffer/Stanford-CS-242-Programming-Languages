/***************
 * NOTE:
 *   You can use `Sig`, `Pkt`, ..., `internal_send_pkts`
 *   which appear in the below `use` declarations,
 *   simply by `Sig`, `Pkt`, ..., `internal_send_pkts` without any prefixes.
 ***************/

#[allow(unused_imports)]
use crate::prob2::msg::{Pkt, Sig};
#[allow(unused_imports)]
use crate::prob2::server::{internal_send_pkts, internal_send_sig, Server};

// TODO: Implement the typestate structs below for the TCP client. You are free to add any fields
// that you think will be helpful to the struct definitions.
// Below shows the signature of the methods needed across the TCP client state machine.
// Note that not all methods may be implemented for every typestate struct.
//
//   pub fn new() -> T
//   pub fn send_syn(self, _: &mut Server) -> Result<T,T>
//   pub fn send_ack(self, _: &mut Server) -> T
//   pub fn send_pkts(self, _: &mut Server, _: &Vec<Pkt>) -> T
//   pub fn send_close(self, _: &mut Server) -> Result<T,T>
//   pub fn ids_sent(&self) -> Vec<u32>
//
// Here T denotes a type. Note that each T can be a different type.
//===== BEGIN_CODE =====//
pub struct Client {}
pub struct Initial {
    sent_packet_ids: Vec<u32>,
}
pub struct Syned {
    sent_packet_ids: Vec<u32>,
}
pub struct SynAcked {
    sent_packet_ids: Vec<u32>,
}
pub struct Closed {
    sent_packet_ids: Vec<u32>,
}

impl Client {
    pub fn new() -> Initial {
        let sent_packet_ids = Vec::new();
        return Initial { sent_packet_ids };
    }
}

impl Initial {

    pub fn send_syn(self, server: &mut Server) -> Result<Syned,Initial> {
        let return_signal: Option<Sig> = internal_send_sig(server, Sig::Syn);
        return match return_signal {
            Some(_) => Ok(Syned { sent_packet_ids: self.sent_packet_ids }),
            None => Err(Initial { sent_packet_ids: self.sent_packet_ids }),
        }
    }

    pub fn ids_sent(&self) -> Vec<u32> {
        return self.sent_packet_ids;
    }
}

impl Syned {

    pub fn send_ack(self, server: &mut Server) -> SynAcked {
        internal_send_sig(server, Sig::Ack);
        return SynAcked { sent_packet_ids: self.sent_packet_ids }
    }

    pub fn ids_sent(&self) -> Vec<u32> {
        return self.sent_packet_ids;
    }

}

impl SynAcked {

    pub fn send_pkts(self, server: &mut Server, packets: &Vec<Pkt>) -> SynAcked {
        let new_sent_packet_ids: Vec<u32> = internal_send_pkts(server, packets);
        new_sent_packet_ids.extend(self.sent_packet_ids);
        return SynAcked { sent_packet_ids: new_sent_packet_ids}
    }

    pub fn send_close(self, server: &mut Server) -> Result<Closed, SynAcked> {
        let return_signal: Option<Sig> = internal_send_sig(server, Sig::Ack);
        match return_signal {
            Some(_) => return Ok(Closed{ sent_packet_ids: self.sent_packet_ids }),
            None => return Err(SynAcked{ sent_packet_ids: self.sent_packet_ids }),
        }
    }

    pub fn ids_sent(&self) -> Vec<u32> {
        return self.sent_packet_ids;
    }

}

impl Closed {

    pub fn send_ack(self, _: &mut Server) -> Initial {
        let sent_packet_ids = Vec::new();
        return Initial { sent_packet_ids}
    }

    pub fn ids_sent(&self) -> Vec<u32> {
        return self.sent_packet_ids;
    }

}

//===== END_CODE =====//
