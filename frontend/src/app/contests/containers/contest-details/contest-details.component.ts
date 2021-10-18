import { Component } from '@angular/core'
import { Observable } from 'rxjs'
import { ContestsStore } from '@/contests/contests.store'
import { Contest, SimpleContestWithFlagResponseTaskParticipant } from '@api/tasks/model'


@Component( {
    selector: 'app-contest-details',
    templateUrl: './contest-details.component.html',
    styleUrls: [ './contest-details.component.scss' ]
} )
export class ContestDetailsComponent
{
    contest$: Observable<SimpleContestWithFlagResponseTaskParticipant | undefined>

    constructor( private contestsStore: ContestsStore )
    {
        this.contest$ = this.contestsStore.contest$
    }

    getTargetClassesDisplay( contest: SimpleContestWithFlagResponseTaskParticipant ): string
    {
        return contest?.contest?.base_contest?.target_classes?.map( item => item.target_class ).join( "," ) + " классы"
    }
}