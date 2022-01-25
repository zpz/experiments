from collections import defaultdict
from typing import Iterable, Sequence


def _internal(components: Iterable[Iterable[int]], n_items:int, n_components: int):
    # Each component is a sequence of items.
    # The items are represented by their indices in the entire set of items
    # across all components, hence all the elements in `components`
    # are integers from 0 up to but not including `n_items`, which
    # is the total numbe of items across all components.

    item_markers = [-1 for _ in range(n_items)]     # Component ID of each item
    component_markers = list(range(n_components))   # Group ID of each component

    for i_component, component_items in enumerate(components):
        for item in component_items:

            # Get the component ID of this item, if it has been marked
            # by a previously-visited component; otherwise it is -1.
            j_component = item_markers[item]

            if j_component < 0:
                # The item has not been marked by a previous component,
                # hence mark it by the current component.
                item_markers[item] = i_component

                # This may or may not start a new group.
                # If the `else` block below has not executed for the current
                # component, then the current component is in a new group
                # (until a later item changes this situation).
                # This new group should have the largest ID possible so far,
                # which is `i_component` (see the `else` block below).
                # The value `component_markers[i_component]` is `i_component`
                # at this moment, hence no update is needed there.
                # Since the current component is the only component in the new
                # group (for now), no update is needed to other component's
                # group IDs.
                #
                # If the `else` block below has ever executed for the current
                # component, then this component belongs to a group with ID
                # `i_component`, which has been taken care of in that block.
                # Nothing else needs to be done about the current item in addition
                # to marking it.
                #
                # Apparently, in any case, the current component belongs to group
                # with ID `i_component`.
            else:
                # The item has been marked by a previous component,
                # with ID `j_component` hence the components `i_component` and
                # `j_component` belong to the same group,
                # because they are "connected" by the current common item.
                #
                # This previous component may share its group with other previous
                # components. All these components as well as the current one
                # share a group. This block ensures that this group gets ID value
                # equal to `i_component`, and all it member components can find
                # this group ID directly or indirectly.

                # Check the group ID of the previous component.
                if component_markers[j_component] == i_component:
                    # A previous item of the current component was also marked by
                    # the component `j_component`. When the previous item was
                    # processed, it updated the group ID to `i_component` for
                    # the component `j_component`, and possibly for other connected
                    # components. All is good now.
                    continue

                # Now the current component has group ID `i_component`, but
                # the connected component `j_component` has group ID that is
                # smaller than `i_component`. Update the group ID of component
                # `j_component` and possibly others that are connected to
                # `j_component`.

                while True:
                    k_group = component_markers[j_component]
                    component_markers[j_component] = i_component
                    # This is the only line that changes `component_markers[idx]`,
                    # and the change is always upwards. Before change, the value
                    # is `idx`. After change, say `component_markers[idx] = jdx`,
                    # the component `idx` shares a group with component `jdx`.
                    # This change happens when and only when a later component
                    # (i.e. `idx < jdx`) sees that the two components are connected.

                    if k_group == j_component:
                        # This suggests the group ID for component `j_component`
                        # was never changed. Until now, the group ID for component
                        # `j_component` has been `j_component`. There may be components
                        # before `j_component` that are connected to `j_component`,
                        # but there are no components after `j_component` that
                        # are connected to it. We have updated
                        # `component_markers[j_component]` to `i_component`.
                        # We do not need to update this for components that are
                        # before `j_component` and connected to it; they will find
                        # their group ID by checking `component_markers[j_component]`.
                        break

                    # The component `j_component` is connected to another component
                    # (whose index is `k_group`) that is after it (`j_component` < `k_group`).
                    # Now that we have updated `component_markers[j_component]`, we
                    # follow the chain to update that of `k_group`.
                    j_component = k_group

    # Now `component_markers` contains the group ID of each component
    # directly or indirectly. The next block makes them all direct.
    for i in reversed(range(n_components)):
        if (k := component_markers[i]) != i:
            # Now it must be that `mark > i`, indicating
            # that the component `i` shares a group
            # with component `mark`. We follow this chain
            # to get the group ID.
            component_markers[i] = component_markers[k]

    return item_markers, component_markers


def connected_components(components: Sequence[Sequence[int]], n_items: int):
    n_components = len(components)
    _, component_markers = _internal(components, n_items, n_components)

    groups = defaultdict(set)
    # Item IDs in each group, indexed by group ID.

    for i_comp, i_grp in enumerate(component_markers):
        groups[i_grp].update(components[i_comp])

    return list(groups.values())

