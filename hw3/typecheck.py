from src.lam import *
from typing import Dict, List, Set, Tuple


def typecheck(prog: Prog) -> List[Type]:
    # Maps from variables to types
    type_context = dict()
    constraints = set()
    definition_types = []
    variable_counter = 0

    # Step 1: Construct constraints & definition types
    for definition in prog.defns:

        definition_type, definition_constraints = generate_constraints(
            type_context=type_context,
            e=definition.e,
            variable_counter=variable_counter)
        definition_types.append(definition_type)
        constraints.update(definition_constraints)
        # TODO: Where do we add a newly declared function?
        type_context[definition.s] = definition_type

    # Step 2: Saturate Constraints
    saturated_constraints = saturate_constraints(constraints=constraints)

    # Step 3: Typecheck
    canonicalize_definitions(
        definition_types=definition_types,
        saturated_constraints=saturated_constraints)

    # If there are no type errors, return a list of Types
    return definition_types


def generate_constraints(type_context: Dict[str, Type],
                         e: Expr,
                         variable_counter: int,
                         ) -> Tuple[Type, Set[Tuple[Type, Type]]]:

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

        # If this variable is not in the type context, then create a new
        # Type and add it to the type context.
        if e.s not in type_context:
            input_type = TpVar(s='a'+str(variable_counter))
            variable_counter += 1
        else:
            input_type = type_context[e.s]

        new_type_context = type_context.copy()
        new_type_context[e.s] = input_type

        output_type, output_type_constraints = generate_constraints(
            type_context=new_type_context,
            e=e.e,
            variable_counter=variable_counter)
        constraints.update(output_type_constraints)
        e_type = TpFunc(a=input_type, b=output_type)

    elif isinstance(e, App):

        # Create new variable type.
        new_type = TpVar(s='a'+str(variable_counter))
        variable_counter += 1

        # Add the new variable to the type context.
        new_type_context = type_context.copy()
        new_type_context[new_type.s] = new_type

        # Recurse on e_1 and e_2.
        function_type, function_type_constraints = generate_constraints(
            type_context=new_type_context,
            e=e.e1,
            variable_counter=variable_counter)

        function_input_type, function_input_type_constraints = generate_constraints(
            type_context=new_type_context,
            e=e.e2,
            variable_counter=variable_counter)

        # Add constraints.
        constraints.update(function_type_constraints)
        constraints.update(function_input_type_constraints)
        new_func_type = TpFunc(a=function_input_type, b=new_type)
        constraints.add((function_type, new_func_type))

        e_type = new_func_type

    else:
        raise NotImplementedError

    return e_type, constraints


def saturate_constraints(constraints: Set[Tuple[Type, Type]],
                         ) -> Set[Tuple[Type, Type]]:

    prev_num_constraints = -1
    saturated_constraints = constraints.copy()

    print(f'Number of Constraints: {len(constraints)}')

    while len(saturated_constraints) != prev_num_constraints:
        prev_num_constraints = len(saturated_constraints)

        # Note: Can't iterate over set while size is changing. Need to duplicate.
        for constraint in saturated_constraints.copy():
            # Reflexive:
            saturated_constraints.add((constraint[1], constraint[0]))

            # Note: Can't iterate over set while size is changing. Need to duplicate.
            for other_constraint in saturated_constraints:
                # Transitive:
                if isinstance(constraint, TpVar) and isinstance(other_constraint, TpVar):
                    if constraint[0] == other_constraint[0]:
                        saturated_constraints.add((constraint[0], other_constraint[1]))
                # Structural:
                if isinstance(constraint, TpFunc) and isinstance(other_constraint, TpFunc):
                    if constraint == other_constraint:
                        saturated_constraints.add((constraint.a, other_constraint.a))
                        saturated_constraints.add((constraint.b, other_constraint.b))

    print(f'Number of Saturated Constraints: {len(saturated_constraints)}')

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
    for definition_type in definition_types:
        definition_types = canonicalize_recursive(
            saturated_constraints=saturated_constraints,
            t=definition_type,
            types_being_canonicalized=types_being_canonicalized)

    return definition_types


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
    elif any([t == constraint[0] for constraint in saturated_constraints]):
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
    else:
        return_type = t

    types_being_canonicalized.remove(t)
    assert return_type is not None
    return return_type
