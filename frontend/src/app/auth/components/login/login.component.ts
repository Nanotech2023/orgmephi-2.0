import { Component, HostListener, OnInit } from '@angular/core'
import { Store } from '@ngrx/store'
import { AuthActions, AuthSelectors, AuthState } from '@/auth/store'
import { Observable } from 'rxjs'
import { ErrorValue, TypeAuthCredentials } from '@/auth/models'
import { fixedHeight } from '@/shared/consts'


@Component( {
    selector: 'app-login',
    templateUrl: './login.component.html',
    styleUrls: [ './login.component.scss' ]
} )
export class LoginComponent implements OnInit
{
    loginAttempt: TypeAuthCredentials
    isAuthenticated$!: Observable<boolean>
    error$!: Observable<ErrorValue[] | null>
    containerHeight: number

    constructor( private readonly store: Store<AuthState.State> )
    {
        this.loginAttempt = { username: '', password: '' }
        this.containerHeight = fixedHeight
    }

    ngOnInit(): void
    {
        this.isAuthenticated$ = this.store.select( AuthSelectors.selectIsAuthenticated )
        this.error$ = this.store.select( AuthSelectors.selectError )
    }

    @HostListener( 'window:resize', [ '$event' ] )
    onResize()
    {
        this.containerHeight = fixedHeight
    }

    login( loginAttemptUser: TypeAuthCredentials ): void
    {
        const authentication = { authentication: { authCredentials: loginAttemptUser } }
        const requestLogin = { authCredentials: loginAttemptUser, rememberMe: true }
        this.store.dispatch( AuthActions.loginAttempt( { requestLogin: requestLogin } ) )
    }

    isValid( loginAttemptUser: TypeAuthCredentials ): boolean
    {
        // TODO enforce email regex check
        return !!( loginAttemptUser.password && loginAttemptUser.username )
    }
}
