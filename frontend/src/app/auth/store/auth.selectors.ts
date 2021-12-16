import { createFeatureSelector, createSelector, MemoizedSelector } from '@ngrx/store'
import { featureKey, State } from '@/auth/store/auth.reducer'
import { User, UserInfo } from '@api/users/models'


export const selectFeature: MemoizedSelector<object, State> = createFeatureSelector<State>( featureKey )

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

export const selectIsPrivileged: MemoizedSelector<State, boolean> = createSelector(
    selectFeature,
    ( state: State ) =>
    {
        if ( !!state.user?.role )
        {
            const userRole = state.user.role
            return [ User.RoleEnum.Admin, User.RoleEnum.System, User.RoleEnum.Creator ].some( item => item === userRole )
        }
        return false
    }
)

export const selectIsConfirmed: MemoizedSelector<State, boolean> = createSelector(
    selectFeature,
    ( state: State ) =>
    {
        if ( !!state.user?.role )
            return state.user.role != User.RoleEnum.Unconfirmed
        return true
    }
)

export const selectUserInfo: MemoizedSelector<State, UserInfo> = createSelector(
    selectFeature,
    ( state: State ) =>
        state.userInfo!
)

export const selectUserPhoto: MemoizedSelector<State, Blob> = createSelector(
    selectFeature,
    ( state: State ) =>
        state.userPhoto!
)

export const selectIsParticipant: MemoizedSelector<State, boolean> = createSelector(
    selectFeature,
    ( state: State ) =>
        state.user?.role === User.RoleEnum.Participant
)

export const selectIsProfileFilled: MemoizedSelector<State, boolean> = createSelector(
    selectFeature,
    ( state: State ) =>
        state.unfilled !== undefined && !!state.unfilled.length
)