import { Component } from '@angular/core'
import { Observable } from 'rxjs'
import { ContestsStore } from '@/contests/contests.store'
import { Contest } from '@api/tasks/model'


@Component( {
    selector: 'app-contest-details',
    templateUrl: './contest-details.component.html',
    styleUrls: [ './contest-details.component.scss' ]
} )
export class ContestDetailsComponent
{
    contest$: Observable<Contest | undefined>

    constructor( private contestsStore: ContestsStore )
    {
        this.contest$ = this.contestsStore.selectedContest
    }
}