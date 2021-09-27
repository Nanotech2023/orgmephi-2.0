import { createFeatureSelector, createSelector, MemoizedSelector } from '@ngrx/store'
import { featureKey, State } from '@/auth/store/auth.reducer'
import { CSRFPairUser, User, UserInfo } from '@api/users/models'


export const selectFeature: MemoizedSelector<object, State> = createFeatureSelector<State>( featureKey )

export const selectApiKeys: MemoizedSelector<State, CSRFPairUser> = createSelector(
    selectFeature,
    ( state: State ) =>
        state.csrfTokens!
)

export const selectIsAuthorized: MemoizedSelector<State, boolean> = createSelector(
    selectFeature,
    ( state: State ) =>
        state.csrfTokens !== null
)

export const selectUser: MemoizedSelector<State, User> = createSelector(
    selectFeature,
    ( state: State ) =>
        state.user!
)
export const selectUserInfo: MemoizedSelector<State, UserInfo> = createSelector(
    selectFeature,
    ( state: State ) =>
        state.userInfo!
)

export const selectIsParticipant: MemoizedSelector<State, boolean> = createSelector(
    selectFeature,
    ( state: State ) =>
        state.user?.role === User.RoleEnum.Participant
)

export const selectAccessToManagePages: MemoizedSelector<State, boolean> = createSelector(
    selectFeature,
    ( state: State ) =>
        state.user?.role === User.RoleEnum.Creator || state.user?.role === User.RoleEnum.Admin || state.user?.role === User.RoleEnum.System
)

export const copy: MemoizedSelector<State, UserInfo> = createSelector(
    selectFeature,
    ( state: State ) =>
    {
        const result: UserInfo = { ...state.userInfo }
        return result
    }
)