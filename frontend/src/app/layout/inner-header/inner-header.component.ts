import { Component, OnInit } from '@angular/core'
import { select, Store } from '@ngrx/store'
import { AuthSelectors, AuthState } from '@/auth/store'
import { Observable } from 'rxjs'
import { User } from '@/auth/api/models'


@Component( {
    selector: 'app-inner-header',
    templateUrl: './inner-header.component.html',
    styleUrls: [ './inner-header.component.scss' ]
} )
export class InnerHeaderComponent implements OnInit
{
    user$!: Observable<User | null>
    isAuthorized$!: Observable<boolean>
    hasAccessToManagePages$!: Observable<boolean>

    constructor( private store: Store<AuthState.State> ) { }

    ngOnInit(): void
    {
        this.isAuthorized$ = this.store.pipe( select( AuthSelectors.selectIsAuthenticated ) )
        this.hasAccessToManagePages$ = this.store.pipe( select( AuthSelectors.selectAccessToManagePages ) )
        this.user$ = this.store.pipe( select( AuthSelectors.selectUserInfo ) )
    }
}
