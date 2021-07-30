import { Component, HostListener, OnInit } from '@angular/core'
import { Store } from '@ngrx/store'
import { AuthActions, AuthSelectors, AuthState } from '@/auth/store'
import { Observable } from 'rxjs'
import { ErrorValue, RequestLogin } from '@/auth/api/models'
import { fixedHeight } from '@/shared/consts'


@Component( {
    selector: 'app-login',
    templateUrl: './login.component.html',
    styleUrls: [ './login.component.scss' ]
} )
export class LoginComponent implements OnInit
{
    loginAttempt: RequestLogin
    isAuthenticated$!: Observable<boolean>
    error$!: Observable<ErrorValue[] | null>
    containerHeight: number

    constructor( private readonly store: Store<AuthState.State> )
    {
        this.loginAttempt = { auth_credentials: { username: '', password: '' }, remember_me: false }
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

    login( loginAttempt: RequestLogin ): void
    {
        this.store.dispatch( AuthActions.loginAttempt( { requestLogin: loginAttempt } ) )
    }

    isValid( loginAttemptUser: RequestLogin ): boolean
    {
        // TODO enforce email regex check
        return !!( loginAttemptUser.auth_credentials.username && loginAttemptUser.auth_credentials.password )
    }
}
