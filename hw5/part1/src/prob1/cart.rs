/***************
 * NOTE:
 *   You can call `internal_login` simply by `internal_login(id, pw)`.
 ***************/

#[allow(unused_imports)]
use crate::prob1::server::internal_login;

// TODO: Implement the following typestate structs. You are free to add any fields to the struct
// definitions.
// Below shows the signature of the methods to be implemented across the cart state machine.
// Note that not all methods may be implemented for every typestate struct.
//
//   pub fn login(_: String, _: String) -> Result<T,()>
//   pub fn add_item(self, _: u32) -> T
//   pub fn clear_items(self) -> T
//   pub fn checkout(self) -> T
//   pub fn cancel(self) -> T
//   pub fn order(self) -> T
//   pub fn acct_num(&self) -> u32
//   pub fn tot_cost(&self) -> u32
//
// Here T denotes a type. Note that each T can be a different type.
//===== BEGIN_CODE =====//
pub struct Cart {  }
pub struct Empty {
    acct_num_val : u32 ,
    tot_cost_val : u32
}
pub struct NonEmpty {
    acct_num_val : u32 ,
    tot_cost_val : u32
}
pub struct Checkout {
    acct_num_val : u32 ,
    tot_cost_val : u32
}

impl Cart {
    pub fn login(id: String, pw: String) -> Result<Empty,()> {
        let user: Option<u32> = internal_login(id, pw);
        match user {
            None => return Err(()),
            Some(val) => return Ok(Empty{acct_num_val: val, tot_cost_val: 0}),
        }
    }
}

impl Empty {
    pub fn add_item(self, cost: u32) -> NonEmpty {
        return NonEmpty{
            acct_num_val: self.acct_num_val,
            tot_cost_val: self.tot_cost_val + cost
        };
    }

    pub fn acct_num(&self) -> u32 {
        return self.acct_num_val
    }

    pub fn tot_cost(&self) -> u32 {
        return self.tot_cost_val
    }
}

impl NonEmpty {

    pub fn add_item(self, cost: u32) -> NonEmpty {
        return NonEmpty{
            acct_num_val: self.acct_num_val,
            tot_cost_val: self.tot_cost_val + cost
        };
    }

    pub fn checkout(self) -> Checkout {
        return Checkout{
            acct_num_val: self.acct_num_val,
            tot_cost_val: self.tot_cost_val
        };
    }

    pub fn clear_items(self) -> Empty {
        return Empty {
            acct_num_val: self.acct_num_val ,
            tot_cost_val: 0
        };
    }

    pub fn acct_num(&self) -> u32 {
        return self.acct_num_val;
    }

    pub fn tot_cost(&self) -> u32 {
        return self.tot_cost_val;
    }
}

impl Checkout {

    pub fn order(self) -> Empty {
        return Empty {
            acct_num_val : self.acct_num_val,
            tot_cost_val : 0,
        }
    }

    pub fn cancel(self) -> NonEmpty {
        return NonEmpty {
            acct_num_val : self.acct_num_val,
            tot_cost_val : self.tot_cost_val,
        }
    }

    pub fn acct_num(&self) -> u32 {
        return self.acct_num_val
    }

    pub fn tot_cost(&self) -> u32 {
        return self.tot_cost_val
    }

}


//===== END_CODE =====//
