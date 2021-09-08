import { NgModule } from '@angular/core'
import { SharedModule } from '@/shared/shared.module'
import { OlympiadsRoutingModule } from '@/olympiads/olympiads.routing.module'
import { HomeComponent } from '@/olympiads/containers/home/home.component'
import { ParticipantComponent } from '@/olympiads/components/participant/participant.component'


const COMPONENTS = [ HomeComponent, ParticipantComponent ]


@NgModule( {
    declarations: COMPONENTS,
    imports: [
        SharedModule,
        OlympiadsRoutingModule
    ]
} )
export class OlympiadsModule {}