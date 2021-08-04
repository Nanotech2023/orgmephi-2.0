import { createFeatureSelector, createSelector, MemoizedSelector } from '@ngrx/store'
import { featureKey, State } from '@/auth/store/auth.reducer'
import { ErrorValue, TypeCSRFPair, TypePersonalInfo, TypeUserInfo } from '@/auth/models'


export const selectFeature: MemoizedSelector<object, State> = createFeatureSelector<State>( featureKey )

export const selectApiKeys: MemoizedSelector<State, TypeCSRFPair | null> = createSelector(
    selectFeature,
    ( state: State ) =>
        state.csrfTokens
)

export const selectIsAuthenticated: MemoizedSelector<State, boolean> = createSelector(
    selectFeature,
    ( state: State ) =>
        state.csrfTokens !== null
)

export const selectUserInfo: MemoizedSelector<State, TypeUserInfo | null> = createSelector(
    selectFeature,
    ( state: State ) =>
        state.userInfo
)

export const selectPersonalInfo: MemoizedSelector<State, TypePersonalInfo | null> = createSelector(
    selectFeature,
    ( state: State ) =>
        state.personalInfo
)

export const selectError: MemoizedSelector<State, ErrorValue[] | null> = createSelector(
    selectFeature,
    ( state: State ) =>
        state.errors
)