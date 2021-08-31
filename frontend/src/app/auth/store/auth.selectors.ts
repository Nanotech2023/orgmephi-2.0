import { createFeatureSelector, createSelector, MemoizedSelector } from '@ngrx/store'
import { featureKey, State } from '@/auth/store/auth.reducer'
import { ErrorValue, CSRFPairUser, User } from '@/auth/api/models'


export const selectFeature: MemoizedSelector<object, State> = createFeatureSelector<State>( featureKey )

export const selectApiKeys: MemoizedSelector<State, CSRFPairUser | null> = createSelector(
    selectFeature,
    ( state: State ) =>
        state.csrfTokens
)

export const selectIsAuthenticated: MemoizedSelector<State, boolean> = createSelector(
    selectFeature,
    ( state: State ) =>
        state.csrfTokens !== null
)

export const selectUserInfo: MemoizedSelector<State, User | null> = createSelector(
    selectFeature,
    ( state: State ) =>
        state.user
)

// export const selectPersonalInfo: MemoizedSelector<State, TypePersonalInfo | null> = createSelector(
//     selectFeature,
//     ( state: State ) =>
//         state.personalInfo
// )

export const selectIsParticipant: MemoizedSelector<State, boolean>= createSelector(
    selectFeature,
    (state: State) =>
        state.user?.role === User.RoleEnum.Participant
)

export const selectAccessToManagePages: MemoizedSelector<State, boolean> = createSelector(
    selectFeature,
    ( state: State ) =>
        state.user?.role === User.RoleEnum.Creator || state.user?.role === User.RoleEnum.Admin || state.user?.role === User.RoleEnum.System
)

export const selectError: MemoizedSelector<State, ErrorValue[] | null> = createSelector(
    selectFeature,
    ( state: State ) =>
        state.errors
)