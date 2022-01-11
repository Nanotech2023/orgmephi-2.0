import { Component } from '@angular/core'
import { OlympiadLocation, SimpleContest } from '@api/tasks/model'
import { Observable } from 'rxjs'
import { TasksService } from '@api/tasks/tasks.service'
import { ActivatedRoute, Router } from '@angular/router'
import { ResponsesService } from '@api/responses/responses.service'
import { UserResponseStatusResponse } from '@api/responses/model'
import { getStatusDisplay, getUserResponseStatusDisplay } from '@/shared/displayUtils'
import { ContestRegistrationStore } from '@/contests/containers/contest-registration/contest-registration.store'
import { environment } from '@environments/environment'


@Component( {
    selector: 'app-contest-registration',
    templateUrl: './contest-registration.component.html',
    styleUrls: [ './contest-registration.component.scss' ],
    providers: [ ContestRegistrationStore ]
} )
export class ContestRegistrationComponent
{
    contest$: Observable<SimpleContest | undefined>
    locations!: Array<OlympiadLocation>
    contestId!: number | null
    contestStatus$!: Observable<UserResponseStatusResponse>

    constructor( private route: ActivatedRoute, private router: Router, private contestRegistrationStore: ContestRegistrationStore, private tasksService: TasksService, private responsesService: ResponsesService )
    {
        this.route.paramMap.subscribe( paramMap =>
        {
            this.contestId = Number( paramMap.get( 'contestId' ) )
            if ( !!this.contestId )
            {
                this.contestRegistrationStore.fetchSingle( this.contestId )
                this.contestStatus$ = this.responsesService.responsesParticipantContestContestIdUserSelfStatusGet( this.contestId )
            }
        } )
        this.contest$ = this.contestRegistrationStore.contest$
        this.tasksService.tasksUnauthorizedLocationAllGet().subscribe( items => this.locations = items.locations )
    }

    onStartClick( contestId: number | undefined ): void
    {
        // TODO allow select other locations
        const locationId = environment.onlineLocationId
        const contestIdNumber = contestId as number
        this.contestRegistrationStore.enroll( {
            contestId: contestIdNumber,
            locationId: locationId
        } )
    }

    accepted( contestStatus: UserResponseStatusResponse ): boolean
    {
        return contestStatus.status === UserResponseStatusResponse.StatusEnum.Accepted
    }

    inProgress( contestStatus: UserResponseStatusResponse ): boolean
    {
        return contestStatus.status === UserResponseStatusResponse.StatusEnum.InProgress
    }

    onContinueClick( contestId: number | undefined ): void
    {
        this.router.navigate( [ `/contests/${ contestId }/assignment` ] )
    }

    onShowResultsClick( contestId: number | undefined ): void
    {
        this.router.navigate( [ `/contests/${ contestId }/assignment-results` ] )
    }

    getUserResponseStatusDisplay( contestStatus: UserResponseStatusResponse ): string
    {
        return getUserResponseStatusDisplay( contestStatus.status )
    }
}
