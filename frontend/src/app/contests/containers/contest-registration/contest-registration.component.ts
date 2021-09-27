import { Component } from '@angular/core'
import { ContestsStore } from '@/contests/contests.store'
import { Contest } from '@api/tasks/model'
import { Observable } from 'rxjs'


@Component( {
    selector: 'app-contest-registration',
    templateUrl: './contest-registration.component.html',
    styleUrls: [ './contest-registration.component.scss' ]
} )
export class ContestRegistrationComponent
{
    contest$: Observable<Contest | undefined>

    constructor( private contestsStore: ContestsStore )
    {
        this.contest$ = contestsStore.selectedContest
    }
}
