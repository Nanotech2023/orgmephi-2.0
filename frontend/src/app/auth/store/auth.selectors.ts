import { createFeatureSelector, createSelector, MemoizedSelector } from '@ngrx/store'
import { featureKey, State } from '@/auth/store/auth.reducer'
import { CSRFPairUser, User, UserInfo } from '@/auth/api/models'


export const selectFeature: MemoizedSelector<object, State> = createFeatureSelector<State>( featureKey )

export const selectApiKeys: MemoizedSelector<State, CSRFPairUser | null> = createSelector(
    selectFeature,
    ( state: State ) =>
        state.csrfTokens
)

export const selectIsAuthorized: MemoizedSelector<State, boolean> = createSelector(
    selectFeature,
    ( state: State ) =>
        state.csrfTokens !== null
)

export const selectUser: MemoizedSelector<State, User | null> = createSelector(
    selectFeature,
    ( state: State ) =>
        state.user
)
export const selectUserInfo: MemoizedSelector<State, UserInfo | null> = createSelector(
    selectFeature,
    ( state: State ) =>
        state.userInfo
)

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