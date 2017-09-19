import logging
import gi
from gi.repository import GLib
from eduvpn.util import error_helper, thread_helper
from eduvpn.remote import list_profiles
from eduvpn.steps.two_way_auth import two_auth_step

logger = logging.getLogger(__name__)


def _background(oauth, meta, builder, window, dialog):
    try:
        profiles = list_profiles(oauth, meta.api_base_uri)
        logger.info("There are {} profiles on {}".format(len(profiles), meta.api_base_uri))
        if len(profiles) > 1:
            GLib.idle_add(lambda: dialog.hide())
            GLib.idle_add(lambda: select_profile_step(builder=builder, profiles=profiles, meta=meta,
                                                      oauth=oauth, window=window))
        elif len(profiles) == 1:
            meta.profile_display_name, meta.profile_id, meta.two_factor = profiles[0]
            two_auth_step(builder=builder, oauth=oauth, meta=meta, window=window)
        else:
            raise Exception("Either there are no VPN profiles defined, or this account does not have the "
                            "required permissions to create a new VPN configurations for any of the "
                            "available profiles.")

    except Exception as e:
        GLib.idle_add(lambda: error_helper(dialog, "Can't fetch profile list", str(e)))
        GLib.idle_add(lambda: dialog.hide())
        raise


def fetch_profile_step(builder, meta, oauth, window):
    """background action step, fetches profiles and shows 'fetching' screen"""
    logger.info("fetching profile step")
    dialog = builder.get_object('fetch-dialog')
    dialog.show_all()

    thread_helper(lambda: _background(oauth, meta, builder, window, dialog))


def select_profile_step(builder, profiles, meta, oauth, window):
    """the profile selection step, doesn't do anything if only one profile"""
    logger.info("opening profile dialog")

    dialog = builder.get_object('profiles-dialog')
    model = builder.get_object('profiles-model')
    selection = builder.get_object('profiles-selection')
    dialog.show_all()
    model.clear()
    print("A")
    [model.append(p) for p in profiles]
    print("B")
    response = dialog.run()
    print("C")
    dialog.hide()

    if response == 0:  # cancel
        logging.info("cancel button pressed")
        return
    else:
        model, treeiter = selection.get_selected()
        if treeiter:
            meta.profile_display_name, meta.profile_id, meta.two_factor = model[treeiter]
            two_auth_step(builder=builder, oauth=oauth, meta=meta, window=window)
        else:
            logger.error("nothing selected")
            return
