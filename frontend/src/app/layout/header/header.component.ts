import { Component, OnInit } from '@angular/core'
import { select, Store } from '@ngrx/store'
import { AuthSelectors, AuthState } from '@/auth/store'
import { Observable } from 'rxjs'
import { CommonUserInfo } from '@/auth/models'


@Component( {
    selector: 'app-header',
    templateUrl: './header.component.html',
    styleUrls: [ './header.component.scss' ]
} )
export class HeaderComponent implements OnInit
{
    isAuthorized$!: Observable<boolean>
    commonUserInfo$!: Observable<CommonUserInfo | null>

    constructor( private store: Store<AuthState.State> ) {}

    ngOnInit(): void
    {
        this.isAuthorized$ = this.store.pipe( select( AuthSelectors.selectIsAuthenticated ) )
        this.commonUserInfo$ = this.store.pipe( select( AuthSelectors.selectCommonUserInfo ) )
    }
}