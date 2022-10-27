from src.lam import *
from typing import Dict, List, Set, Tuple

variable_counter = 0


def typecheck(prog: Prog) -> List[Type]:

    global variable_counter
    # Make sure to reset variable counter per program.
    variable_counter = 0

    # Maps from variables to types
    type_context = dict()
    constraints = set()
    definition_types = []

    # Step 1: Construct constraints & definition types
    for definition in prog.defns:
        definition_type, definition_constraints = generate_constraints(
            type_context=type_context,
            e=definition.e)
        definition_types.append(definition_type)
        constraints.update(definition_constraints)
        type_context[definition.s] = definition_type

    # Step 2: Saturate Constraints
    saturated_constraints = saturate_constraints(constraints=constraints)

    # Step 3: Typecheck
    substituted_definition_types = canonicalize_definitions(
        definition_types=definition_types,
        saturated_constraints=saturated_constraints)

    # If there are no type errors, return a list of Types
    return substituted_definition_types


def generate_constraints(type_context: Dict[str, Type],
                         e: Expr,
                         ) -> Tuple[Type, Set[Tuple[Type, Type]]]:

    global variable_counter

    # Start with no additional constraints, then add as necessary.
    constraints = set()

    if isinstance(e, IntConst):
        e_type = TpInt()
    elif isinstance(e, Var):
        if e.s in CONSTS:
            e_type = CONSTS[e.s]
        elif e.s not in type_context:
            raise TypecheckingError(f"Variable {e.s} is not defined.")
        else:
            e_type = type_context[e.s]

    elif isinstance(e, Lam):

        fresh_var_type = TpVar(s='a' + str(variable_counter))
        variable_counter += 1

        copied_type_context = type_context.copy()
        copied_type_context[e.s] = fresh_var_type

        output_type, output_type_constraints = generate_constraints(
            type_context=copied_type_context,
            e=e.e)
        constraints.update(output_type_constraints)
        e_type = TpFunc(a=fresh_var_type, b=output_type)

    elif isinstance(e, App):

        # Create new variable type.
        fresh_var_type = TpVar(s='a' + str(variable_counter))
        variable_counter += 1

        # Recurse on e_1 and e_2.
        function_type, function_type_constraints = generate_constraints(
            type_context=type_context,
            e=e.e1)

        function_input_type, function_input_type_constraints = generate_constraints(
            type_context=type_context,
            e=e.e2)

        # Add constraints.
        constraints.update(function_type_constraints)
        constraints.update(function_input_type_constraints)
        new_func_type = TpFunc(a=function_input_type, b=fresh_var_type)
        constraints.add((function_type, new_func_type))

        e_type = fresh_var_type

    else:
        raise NotImplementedError

    return e_type, constraints


def saturate_constraints(constraints: Set[Tuple[Type, Type]],
                         ) -> Set[Tuple[Type, Type]]:
    prev_num_constraints = -1
    saturated_constraints = constraints.copy()

    while len(saturated_constraints) != prev_num_constraints:

        prev_num_constraints = len(saturated_constraints)

        # Note: Can't iterate over set while size is changing. Need to duplicate.
        for constraint in saturated_constraints.copy():

            # Reflexive:
            if isinstance(constraint[1], TpVar):
                saturated_constraints.add((constraint[1], constraint[0]))

            # Note: Can't iterate over set while size is changing. Need to duplicate.
            if isinstance(constraint[0], TpVar):
                for other_constraint in saturated_constraints.copy():
                    # Transitive:
                    if isinstance(other_constraint[0], TpVar):
                        if constraint[0] == other_constraint[0]:
                            saturated_constraints.add((constraint[1], other_constraint[1]))

            # Structural:
            # Note: Somehow TpFunc may induce an error.
            if isinstance(constraint[0], TpFunc) and isinstance(constraint[1], TpFunc):
                # Function inputs must match.
                saturated_constraints.add((constraint[0].a, constraint[1].a))
                # Function outputs must match.
                saturated_constraints.add((constraint[0].b, constraint[1].b))

    return saturated_constraints


def canonicalize_definitions(definition_types: List[Type],
                             saturated_constraints: Set[Tuple[Type, Type]]) -> List[Type]:
    # We first need to check that there is no equality between int and a function type. If there is, the constraints
    # have no solution, and the program is ill-typed.
    for constraint in saturated_constraints:
        if isinstance(constraint[0], TpInt) and isinstance(constraint[1], TpFunc):
            raise TypecheckingError(f"Constraint {constraint} has TpInt == TpFunc")

    # Canonicalize recursive.
    types_being_canonicalized = set()
    substituted_definition_types = []
    for definition_type in definition_types:
        substituted_definition_type = canonicalize_recursive(
            saturated_constraints=saturated_constraints,
            t=definition_type,
            types_being_canonicalized=types_being_canonicalized)
        substituted_definition_types.append(substituted_definition_type)

    return substituted_definition_types


def canonicalize_recursive(saturated_constraints: Set[Tuple[Type, Type]],
                           t: Type,
                           types_being_canonicalized: Set[Type]) -> Type:
    if t in types_being_canonicalized:
        raise TypecheckingError(f"Infinite loop.")
    else:
        types_being_canonicalized.add(t)

    return_type = None
    if isinstance(t, TpInt):
        return_type = t
    elif isinstance(t, TpFunc):
        canonicalized_input = canonicalize_recursive(
            saturated_constraints=saturated_constraints,
            t=t.a,
            types_being_canonicalized=types_being_canonicalized)
        canonicalized_output = canonicalize_recursive(
            saturated_constraints=saturated_constraints,
            t=t.b,
            types_being_canonicalized=types_being_canonicalized,
        )
        return_type = TpFunc(a=canonicalized_input, b=canonicalized_output)
    else:
        flag = False
        for constraint in saturated_constraints:
            if t == constraint[0] and not isinstance(constraint[1], TpVar):
                return_type = canonicalize_recursive(
                    saturated_constraints=saturated_constraints,
                    t=constraint[1],
                    types_being_canonicalized=types_being_canonicalized)
                flag = True
            if t == constraint[0] and constraint[0].s < t.s:
                return_type = canonicalize_recursive(
                    saturated_constraints=saturated_constraints,
                    t=constraint[1],
                    types_being_canonicalized=types_being_canonicalized)
                flag = True
        if not flag:
            return_type = t

    types_being_canonicalized.remove(t)
    assert return_type is not None
    return return_type
