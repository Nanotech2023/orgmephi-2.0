import { NgModule } from '@angular/core'
import { SharedModule } from '@/shared/shared.module'
import { ProfileRoutingModule } from '@/profile/profile.routing.module'
import { ProfileViewComponent } from '@/profile/components/profile-view/profile-view.component'


const COMPONENTS = [
    ProfileViewComponent
]


@NgModule( {
    declarations: COMPONENTS,
    imports: [
        SharedModule,
        ProfileRoutingModule
    ]
} )
export class ProfileModule {}
