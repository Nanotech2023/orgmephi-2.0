import { Component, Input } from '@angular/core'
import { UserExternalDataResponseTaskParticipant } from '@api/tasks/model'


@Component( {
    selector: 'app-contest-details-stage5',
    templateUrl: './contest-details-stage5.component.html',
    styleUrls: [ './contest-details-stage5.component.scss' ]
} )
export class ContestDetailsStage5Component
{
    @Input() contestFinalStageData!: UserExternalDataResponseTaskParticipant
}