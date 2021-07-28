import { Component } from '@angular/core'
import { footerHeight, headerHeight } from '@/shared/consts'


@Component( {
    selector: 'app-participant',
    templateUrl: './participant.component.html',
    styleUrls: [ './participant.component.scss' ]
} )
export class ParticipantComponent
{
    calculateHeight(): number
    {
        return footerHeight + headerHeight
    }
}