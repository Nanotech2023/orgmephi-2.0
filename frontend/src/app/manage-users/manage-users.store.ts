import { Injectable } from '@angular/core'
import { ComponentStore, tapResponse } from '@ngrx/component-store'
import { RequestRegistrationSchool, ResponseUserAll, TypeUserInfo } from '@/auth/api/models'
import { EMPTY, Observable } from 'rxjs'
import { catchError, concatMap } from 'rxjs/operators'
import { AuthService } from '@/auth/api/auth.service'
import { CallState, getError, LoadingState } from '@/shared/callState'


export interface ManageUsersState
{
    users: Array<TypeUserInfo>
    callState: CallState
}


@Injectable()
export class ManageUsersStore extends ComponentStore<ManageUsersState>
{
    constructor( private authService: AuthService )
    {
        super( { users: [], callState: LoadingState.INIT } )
    }

    readonly users$: Observable<TypeUserInfo[]> = this.select( state => state.users )
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

    readonly updateUsers = this.updater( ( state: ManageUsersState, userInfo: TypeUserInfo ) =>
        ( {
            ...state,
            error: "",
            users: [ ...state.users, userInfo ]
        } ) )

    // EFFECTS
    readonly reload = this.effect( ( dummy$: Observable<boolean> ) =>
        dummy$.pipe(
            concatMap( ( dummy: boolean ) =>
                {
                    this.setLoading()
                    return this.authService.userAllGet().pipe(
                        tapResponse(
                            ( response: ResponseUserAll ) =>
                                this.setState( { users: response.users, callState: LoadingState.LOADED } ),
                            ( error: string ) => this.updateError( error )
                        ),
                        catchError( () => EMPTY )
                    )
                }
            )
        ) )


    readonly add = this.effect( ( requestRegistration$: Observable<RequestRegistrationSchool> ) =>
        requestRegistration$.pipe(
            concatMap( ( requestRegistration: RequestRegistrationSchool ) =>
            {
                this.setLoading()
                return this.authService.registerSchoolPost( requestRegistration ).pipe(
                    tapResponse(
                        typeUserInfo =>
                        {
                            this.setLoaded()
                            this.updateUsers( typeUserInfo )
                        },
                        ( error: string ) => this.updateError( error )
                    ),
                    catchError( () => EMPTY )
                )
            } )
        ) )

    readonly edit = this.effect( ( userInfo$: Observable<TypeUserInfo> ) =>
        userInfo$.pipe(
            concatMap( ( userInfo: TypeUserInfo ) =>
            {
                this.setLoading()
                // @ts-ignore
                return this.authService.userUserIdPersonalPatch( userInfo ).pipe(
                    tapResponse(
                        typeUserInfo =>
                        {
                            this.setLoaded()
                            this.updateUsers( typeUserInfo )
                        },
                        ( error: string ) => this.updateError( error )
                    ),
                    catchError( () => EMPTY )
                )
            } )
        ) )
}