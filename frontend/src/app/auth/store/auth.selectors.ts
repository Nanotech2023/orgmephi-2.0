import { createFeatureSelector, createSelector, MemoizedSelector } from '@ngrx/store'
import { featureKey, State } from '@/auth/store/auth.reducer'
import { AuthResult, RegisterResult, UserAuth, UserRegister } from '@/auth/models'


export const selectFeature: MemoizedSelector<object, State> = createFeatureSelector<State>( featureKey )

export const selectAuthResult: MemoizedSelector<State, AuthResult> = createSelector(
    selectFeature,
    ( state: State ) =>
        state.authResult
)

export const selectIsAuthenticated: MemoizedSelector<State, boolean> = createSelector(
    selectFeature,
    ( state: State ) =>
        state.authResult.isSuccessful
)

export const selectUser: MemoizedSelector<State, UserAuth | null> = createSelector(
    selectFeature,
    ( state: State ) =>
        state.user
)

export const selectRegistration: MemoizedSelector<State, UserRegister> = createSelector(
    selectFeature,
    ( state: State ) =>
        state.registration
)
export const selectIsRegistered: MemoizedSelector<State, boolean> = createSelector(
    selectFeature,
    ( state: State ) =>
        state.registrationResult.isSuccessful
)