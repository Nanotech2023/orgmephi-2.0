import { NgModule } from '@angular/core'
import { SharedModule } from '@/shared/shared.module'
import { OlympiadsRoutingModule } from '@/olympiads/olympiads.routing.module'
import { OlympiadListComponent } from '@/olympiads/containers/olympiad-list/olympiad-list.component'
import { ParticipantComponent } from '@/olympiads/components/participant/participant.component'
import { OlympiadDetailsComponent } from '@/olympiads/containers/olympiad-details/olympiad-details.component'


const COMPONENTS = [ OlympiadListComponent, ParticipantComponent, OlympiadDetailsComponent ]


@NgModule( {
    declarations: COMPONENTS,
    imports: [
        SharedModule,
        OlympiadsRoutingModule
    ]
} )
export class OlympiadsModule {}