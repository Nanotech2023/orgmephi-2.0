import { Component } from '@angular/core'
import { Observable } from 'rxjs'
import { ContestsStore } from '@/contests/contests.store'
import { Contest, SimpleContest, SimpleContestWithFlagResponseTaskParticipant } from '@api/tasks/model'
import { ActivatedRoute } from '@angular/router'
import { getClassesForDisplay, getStatusDisplay } from '@/shared/displayUtils'


@Component( {
    selector: 'app-contest-details',
    templateUrl: './contest-details.component.html',
    styleUrls: [ './contest-details.component.scss' ]
} )
export class ContestDetailsComponent
{
    contest$: Observable<SimpleContest | undefined>
    contestId!: number | null

    constructor( private route: ActivatedRoute, private contestsStore: ContestsStore )
    {
        this.route.paramMap.subscribe( paramMap =>
        {
            this.contestId = Number( paramMap.get( 'contestId' ) )
            if ( !!this.contestId )
            {
                this.contestsStore.fetchSingle( this.contestId )
            }
        } )
        this.contest$ = this.contestsStore.contest$
    }

    getTargetClassesDisplay( contest: SimpleContest ): string
    {
        return getClassesForDisplay( contest )
    }

    getStatusForDisplay( contest: SimpleContest )
    {
        return getStatusDisplay( contest )
    }
}