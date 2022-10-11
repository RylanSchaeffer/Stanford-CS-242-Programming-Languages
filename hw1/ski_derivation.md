# SKI Derivation

## Not

We want `not B => B F T`. Abstracting, we have:

$$
\begin{align*}
not &= A((B F) T, B)\\
&= (S A(B F, B)) A(T, B)\\
&= (S ((S A(B, B)) A(F, B))) (K T)\\
&= (S ((S I) (K F))) (K T)
\end{align*}
$$

## Or

We want `or B1 B2 => B1 T B2`. Abstracting first w.r.t. `B1`, we have

$$
\begin{align*}
or B_1 B_2 &= A(B_1 T B_2, B_2)\\
&= ((S A(B_1, B_2)) A(T B_2, B_2))\\
&= ((S (K B_1)) (S A(T, B_2) A(B_2, B_2)))\\
&= ((S (K B_1)) (S A(T, B_2) A(B_2, B_2)))\\
\end{align*}
$$

## And

## Is Odd

$$
\begin{align*}
is_odd N &= \\
&= 
\end{align*}
$$