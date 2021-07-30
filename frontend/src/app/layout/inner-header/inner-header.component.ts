import { Component, OnInit } from '@angular/core'
import { select, Store } from '@ngrx/store'
import { AuthSelectors, AuthState } from '@/auth/store'
import { Observable } from 'rxjs'
import { TypeUserInfo } from '@/auth/api/models'
import { AuthServiceReal } from '@/auth/api/auth.service.real'


@Component( {
    selector: 'app-inner-header',
    templateUrl: './inner-header.component.html',
    styleUrls: [ './inner-header.component.scss' ]
} )
export class InnerHeaderComponent implements OnInit
{
    userInfo!: Observable<TypeUserInfo | null>
    isAuthorized$!: Observable<boolean>

    constructor( private store: Store<AuthState.State>, private service: AuthServiceReal ) { }

    ngOnInit(): void
    {
        this.isAuthorized$ = this.store.pipe( select( AuthSelectors.selectIsAuthenticated ) )
        this.userInfo = this.service.userSelfGet()
    }
}
