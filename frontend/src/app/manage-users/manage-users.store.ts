import { Injectable } from '@angular/core'
import { ComponentStore, tapResponse } from '@ngrx/component-store'
import { SchoolRegistrationRequestUser, User, UserFull, UserFullListResponseUser } from '@/auth/api/models'
import { EMPTY, Observable } from 'rxjs'
import { catchError, concatMap } from 'rxjs/operators'
import { AuthService } from '@/auth/api/auth.service'
import { CallState, getError, LoadingState } from '@/shared/callState'


export interface ManageUsersState
{
    users: Array<UserFull>
    callState: CallState
}


@Injectable()
export class ManageUsersStore extends ComponentStore<ManageUsersState>
{
    constructor( private authService: AuthService )
    {
        super( { users: [], callState: LoadingState.INIT } )
    }

    readonly users$: Observable<User[]> = this.select( state => state.users )
    private readonly loading$: Observable<boolean> = this.select( state => state.callState === LoadingState.LOADING )
    private readonly error$: Observable<string | null> = this.select( state => getError( state.callState ) )

    // UPDATERS
    readonly updateError = this.updater( ( state: ManageUsersState, error: string ) =>
        ( {
            ...state,
            callState: { errorMessage: error }
        } ) )

    readonly setLoading = this.updater( ( state: ManageUsersState ) =>
        ( {
            ...state,
            callState: LoadingState.LOADING
        } ) )

    readonly setLoaded = this.updater( ( state: ManageUsersState ) =>
        ( {
            ...state,
            callState: LoadingState.LOADED
        } ) )

    readonly updateUsers = this.updater( ( state: ManageUsersState, user: User ) =>
        ( {
            ...state,
            error: "",
            users: [ ...state.users, user ]
        } ) )

    // EFFECTS
    readonly reload = this.effect( () =>
    {
        this.setLoading()
        return this.authService.userCreatorUserFullAllGet().pipe(
            tapResponse( ( response: UserFullListResponseUser ) =>
                    this.setState( { users: response.users, callState: LoadingState.LOADED } ),
                ( error: string ) => this.updateError( error )
            ),
            catchError( () => EMPTY )
        )
    } )


    readonly add = this.effect( ( requestRegistration$: Observable<SchoolRegistrationRequestUser> ) =>
        requestRegistration$.pipe(
            concatMap( ( requestRegistration: SchoolRegistrationRequestUser ) =>
            {
                this.setLoading()
                return this.authService.userRegistrationSchoolPost( requestRegistration ).pipe(
                    tapResponse(
                        () => this.reload(),
                        ( error: string ) => this.updateError( error )
                    ),
                    catchError( () => EMPTY )
                )
            } )
        ) )

    readonly edit = this.effect( ( user$: Observable<User> ) =>
        user$.pipe(
            concatMap( ( user: User ) =>
            {
                this.setLoading()
                // @ts-ignore
                // TODO
                return this.authService.userAdminSchoolUserIdPatch( user.id, user ).pipe(
                    tapResponse(
                        () => this.reload(),
                        ( error: string ) => this.updateError( error )
                    ),
                    catchError( () => EMPTY )
                )
            } )
        ) )
}