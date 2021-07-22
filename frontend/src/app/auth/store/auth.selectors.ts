import { createFeatureSelector, createSelector, MemoizedSelector } from '@ngrx/store'
import { featureKey, State } from '@/auth/store/auth.reducer'
import { AuthResponse, CommonUserInfo, PersonalInfo } from '@/auth/models'


export const selectFeature: MemoizedSelector<object, State> = createFeatureSelector<State>( featureKey )

export const selectApiKeys: MemoizedSelector<State, AuthResponse | null> = createSelector(
    selectFeature,
    ( state: State ) =>
        state.apiKeys
)

export const selectIsAuthenticated: MemoizedSelector<State, boolean> = createSelector(
    selectFeature,
    ( state: State ) =>
        state.apiKeys !== null
)

export const selectCommonUserInfo: MemoizedSelector<State, CommonUserInfo | null> = createSelector(
    selectFeature,
    ( state: State ) =>
        state.commonUserInfo
)

export const selectPersonalInfo: MemoizedSelector<State, PersonalInfo | null> = createSelector(
    selectFeature,
    ( state: State ) =>
        state.personalInfo
)

export const selectError: MemoizedSelector<State, string | null> = createSelector(
    selectFeature,
    ( state: State ) =>
        state.error
)