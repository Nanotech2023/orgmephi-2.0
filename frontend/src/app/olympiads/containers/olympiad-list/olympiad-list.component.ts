import { Component, OnInit } from '@angular/core'
import { select, Store } from '@ngrx/store'
import { AuthSelectors, AuthState } from '@/auth/store'
import { Observable } from 'rxjs'


@Component( {
    selector: 'app-home',
    templateUrl: './olympiad-list.component.html',
    styleUrls: [ './olympiad-list.component.scss' ]
} )
export class OlympiadListComponent implements OnInit
{
    isParticipant$!: Observable<boolean>

    constructor( private store: Store<AuthState.State> ) {}

    ngOnInit(): void
    {
        this.isParticipant$ = this.store.pipe( select( AuthSelectors.selectIsParticipant ) )
    }
}
