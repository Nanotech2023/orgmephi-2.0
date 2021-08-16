import { Component, OnInit } from '@angular/core'
import { select, Store } from '@ngrx/store'
import { AuthSelectors, AuthState } from '@/auth/store'
import { Observable } from 'rxjs'


@Component( {
    selector: 'app-home',
    templateUrl: './home.component.html',
    styleUrls: [ './home.component.scss' ]
} )
export class HomeComponent implements OnInit
{
    isParticipant$!: Observable<boolean>

    constructor( private store: Store<AuthState.State> ) {}

    ngOnInit(): void
    {
        this.isParticipant$ = this.store.pipe( select( AuthSelectors.selectIsParticipant ) )
    }
}
