import { Component, OnInit } from '@angular/core'
import { select, Store } from '@ngrx/store'
import { AuthSelectors, AuthState } from '@/auth/store'
import { Observable } from 'rxjs'
import { User, UserInfo } from '@/auth/api/models'


@Component( {
    selector: 'app-inner-header',
    templateUrl: './inner-header.component.html',
    styleUrls: [ './inner-header.component.scss' ]
} )
export class InnerHeaderComponent implements OnInit
{
    isAuthorized$!: Observable<boolean>
    hasAccessToManagePages$!: Observable<boolean>
    user$!: Observable<User | null>
    userInfo$!: Observable<UserInfo | null>

    constructor( private store: Store<AuthState.State> ) { }

    ngOnInit(): void
    {
        this.isAuthorized$ = this.store.pipe( select( AuthSelectors.selectIsAuthorized ) )
        this.hasAccessToManagePages$ = this.store.pipe( select( AuthSelectors.selectAccessToManagePages ) )
        this.user$ = this.store.pipe( select( AuthSelectors.selectUser ) )
        this.userInfo$ = this.store.pipe( select( AuthSelectors.selectUserInfo ) )
    }
}
